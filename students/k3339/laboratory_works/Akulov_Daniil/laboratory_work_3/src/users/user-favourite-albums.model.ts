import {Column, DataType, ForeignKey, Model, Table} from "sequelize-typescript";
import {ApiProperty} from "@nestjs/swagger";
import {User} from "./users.model";
import {Album} from "../albums/albums.model";

@Table({tableName: 'user_favourite_albums', updatedAt: false})
export class UserFavouriteAlbums extends Model<UserFavouriteAlbums> {
    @ApiProperty({example: 1})
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number

    @ForeignKey(() => User)
    @Column({type: DataType.INTEGER})
    userId: number

    @ForeignKey(() => Album)
    @Column({type: DataType.INTEGER})
    albumId: number
}