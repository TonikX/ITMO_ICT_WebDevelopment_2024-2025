import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { User } from '@/src/users/entities/user.entity/user.entity';

import { Repository } from 'typeorm';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async findByEmail(email: string): Promise<User | undefined> {
    return this.usersRepository.findOne({ where: { email } });
  }

  async create(userData: Partial<User>): Promise<User> {
    const user = this.usersRepository.create(userData);
    return this.usersRepository.save(user);
  }

  async findOneById(id: number): Promise<User> {
    const user = await this.usersRepository.findOne({ where: { id } });
    if (!user) {
      throw new NotFoundException('Пользователь не найден');
    }
    return user;
  }

  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  async blockUser(id: number): Promise<User> {
    const user = await this.findOneById(id);
    user.isBlocked = true;
    return this.usersRepository.save(user);
  }

  async remove(id: number): Promise<void> {
    const result = await this.usersRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException('Пользователь не найден');
    }
  }
}
