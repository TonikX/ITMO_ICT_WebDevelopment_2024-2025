import {BelongsToMany, Column, DataType, Model, Table} from "sequelize-typescript";
import {ApiProperty} from "@nestjs/swagger";
import {Artist} from "../artists/artists.model";
import {UserBlockedArtists} from "./user-blocked-artists.model";
import {UserFavouriteAlbums} from "./user-favourite-albums.model";
import {Album} from "../albums/albums.model";

interface UserCreationAttrs{
    username:string;
    firstname:string;
    lastname:string;
    password:string;
}

@Table({tableName: 'users'})
export class User extends Model<User, UserCreationAttrs> {
    @ApiProperty({example: 1})
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number

    @ApiProperty({example: 'rileyparker'})
    @Column({type: DataType.STRING(20), unique: true, allowNull: false})
    username: string

    @ApiProperty({example: 'Riley'})
    @Column({type: DataType.STRING(20), allowNull: false})
    firstname: string

    @ApiProperty({example: 'Parker'})
    @Column({type: DataType.STRING(20), defaultValue: ''})
    lastname: string

    @ApiProperty({example: 'password123'})
    @Column({type: DataType.STRING, allowNull: false})
    password: string

    @ApiProperty({example: 'Profile desc :)'})
    @Column({type: DataType.STRING(140), defaultValue: ''})
    description: string

    @ApiProperty({example: 'ovbisut94ueslxzjvo.png'})
    @Column({type: DataType.STRING, defaultValue: ''})
    avatarURL: string

    @BelongsToMany(() => Artist, () => UserBlockedArtists)
    blockedArtists: Artist[]

    @BelongsToMany(() => Album, () => UserFavouriteAlbums)
    favouriteAlbums: Album[]
}