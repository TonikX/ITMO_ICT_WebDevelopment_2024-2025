import {ApiProperty} from "@nestjs/swagger";
import {IsString, Length} from "class-validator";
import {LoginUserDto} from "./login-user.dto";

export class CreateUserDto extends LoginUserDto {
    @ApiProperty({example: 'Riley'})
    @IsString({message: 'Firstname must be string'})
    @Length(1, 20, {message: 'Firstname length must be between 1 and 20'})
    readonly firstname: string;

    @ApiProperty({example: 'Parker'})
    @IsString({message: 'Lastname must be string'})
    @Length(0, 20, {message: 'Lastname length must be less then 20'})
    readonly lastname: string;
}